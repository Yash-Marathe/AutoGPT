"use strict";

var Module = {};

var ENVIRONMENT_IS_NODE =
  typeof process === "object" &&
  typeof process.versions === "object" &&
  typeof process.versions.node === "string";

if (ENVIRONMENT_IS_NODE) {
  var nodeWorkerThreads = require("worker_threads");
  var parentPort = nodeWorkerThreads.parentPort;

  parentPort.on("message", (data) => {
    onmessage({ data: data });
  });

  var fs = require("fs");

  Object.assign(global, {
    self: global,
    require: require,
    Module: Module,
    location: { href: __filename },
    Worker: nodeWorkerThreads.Worker,
    importScripts: (file) => {
      const source = fs.readFileSync(file, "utf8") + "//# sourceURL=" + file;
      eval(source);
    },
    postMessage: (msg) => {
      parentPort.postMessage(msg);
    },
    performance: global.performance || { now: () => Date.now() },
  });
}

var initializedJS = false;
var pendingNotifiedProxyingQueues = [];

function threadPrintErr(...text) {
  if (ENVIRONMENT_IS_NODE) {
    fs.writeSync(2, text.join(" ") + "\n");
    return;
  }
  console.error(text.join(" "));
}

function threadAlert(...text) {
  const message = text.join(" ");
  postMessage({ cmd: "alert", text: message, threadId: Module["_pthread_self"]() });
}

self.alert = threadAlert;

Module["instantiateWasm"] = (info, receiveInstance) => {
  const module = Module["wasmModule"];
  Module["wasmModule"] = null;
  const instance = new WebAssembly.Instance(module, info);
  return receiveInstance(instance);
};

self.onunhandledrejection = (e) => {
  throw e.reason ?? e;
};

function handleMessage(e) {
  try {
    if (e.data.cmd === "load") {
      const messageQueue = [];
      self.onmessage = (msg) => messageQueue.push(msg);
      self.startWorker = (instance) => {
        Module = instance;
        postMessage({ cmd: "loaded" });
        for (let msg of messageQueue) {
          handleMessage(msg);
        }
        self.onmessage = handleMessage;
      };
      Module["wasmModule"] = e.data.wasmModule;
      for (const handler of e.data.handlers) {
        Module[handler] = (...args) => {
          postMessage({
            cmd: "callHandler",
            handler: handler,
            args: [...args],
          });
        };
      }
      Module["wasmMemory"] = e.data.wasmMemory;
      Module["buffer"] = Module["wasmMemory"].buffer;
      Module["ENVIRONMENT_IS_PTHREAD"] = true;

      if (typeof e.data.urlOrBlob === "string") {
        importScripts(e.data.urlOrBlob);
      } else {
        const objectUrl = URL.createObjectURL(e.data.urlOrBlob);
        importScripts(objectUrl);
        URL.revokeObjectURL(objectUrl);
      }

      skwasm(Module);
    } else if (e.data.cmd === "run") {
      Module["__emscripten_thread_init"](
        e.data.pthread_ptr,
        0,
        0,
        1
      );
      Module["establishStackSpace"]();
      Module["PThread"].receiveObjectTransfer(e.data);
      Module["PThread"].threadInitTLS();

      if (!initializedJS) {
        pendingNotifiedProxyingQueues.forEach((queue) => {
          Module["executeNotifiedProxyingQueue"](queue);
        });
        pendingNotifiedProxyingQueues = [];
        initializedJS = true;
      }

      try {
        Module["invokeEntryPoint"](e.data.start_routine, e.data.arg);
      } catch (ex) {
        if (ex !== "unwind") {
          throw ex;
        }
      }
    } else if (e.data.cmd === "cancel") {
      if (Module["_pthread_self"]()) {
        Module["__emscripten_thread_exit"](-1);

