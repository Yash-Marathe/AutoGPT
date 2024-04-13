/**
 * Toastify.js - A simple JavaScript library for creating toast messages
 * @version 1.9.3
 * @license MIT
 * @author Varun A P
 */

class Toastify {
  constructor(options) {
    this.options = this.getDefaultOptions();
    this.setOptions(options);
    this.toastElement = null;
  }

  getDefaultOptions() {
    return {
      text: "Hi there!",
      node: null,
      duration: 3000,
      selector: null,
      callback: () => {},
      destination: null,
      newWindow: false,
      close: false,
      gravity: "toastify-bottom",
      positionLeft: false,
      position: "",
      backgroundColor: null,
      avatar: null,
      className: "",
      stopOnFocus: void 0,
      onClick: null,
      offset: { x: 0, y: 0 },
    };
  }

  setOptions(options) {
    Object.keys(this.options).forEach((key) => {
      if (options.hasOwnProperty(key)) {
        this.options[key] = options[key];
      }
    });

    if (this.options.positionLeft) {
      console.warn(
        "Property `positionLeft` will be deprecated in further versions. Please use `position` instead."
      );
    }

    this.options.offset = this.normalizeOffset(this.options.offset);
  }

  normalizeOffset(offset) {
    if (offset && typeof offset === "object") {
      return {
        x: this.normalizeOffsetValue(offset.x),
        y: this.normalizeOffsetValue(offset.y),
      };
    }

    return { x: 0, y: 0 };
  }

  normalizeOffsetValue(value) {
    if (typeof value === "string" && !isNaN(value)) {
      return value + "px";
    }

    return value;
  }

  buildToast() {
    if (!this.options) {
      throw new Error("Toastify is not initialized");
    }

    const t = document.createElement("div");
    t.className = `toastify on ${this.options.className}`;

    if (this.options.position) {
      t.className += ` toastify-${this.options.position}`;
    } else if (this.options.positionLeft) {
      t.className += " toastify-left";
    } else {
      t.className += " toastify-right";
    }

    t.className += ` ${this.options.gravity}`;

    if (this.options.backgroundColor) {
      t.style.background = this.options.backgroundColor;
    }

    if (this.options.node && this.options.node.nodeType === Node.ELEMENT_NODE) {
      t.appendChild(this.options.node);
    } else {
      t.innerHTML = this.options.text;
    }

    if (this.options.avatar) {
      const avatar = document.createElement("img");
      avatar.src = this.options.avatar;
      avatar.className = "toastify-avatar";

      if (this.options.position === "left" || this.options.positionLeft) {
        t.insertAdjacentElement("afterbegin", avatar);
      } else {
        t.appendChild(avatar);
      }
    }

    if (this.options.close) {
      const closeButton = document.createElement("span");
      closeButton.innerHTML = "&#10006;";
      closeButton.className = "toast-close";

      closeButton.addEventListener("click", () => {
        this.removeElement(this.toastElement);
        window.clearTimeout(this.toastElement.timeOutValue);
      });

      if (
        window.innerWidth > 0
        ? window.innerWidth
        : screen.width <= 360
      ) {
        t.insertAdjacentElement("afterbegin", closeButton);
      } else {
        t.appendChild(closeButton);
      }
    }

    if (
      this.options.stopOnFocus &&
      this.options.duration > 0
    ) {
      t.addEventListener("mouseover", () => {
        window.clearTimeout(t.timeOutValue);
      });

      t.addEventListener("mouseleave", () => {
        t.timeOutValue = window.setTimeout(
          () => this.removeElement(this.toastElement),
          this.options.duration
        );
      });
    }

    if (
      this.options.destination &&
      typeof this.options.destination === "string"
    ) {
      t.addEventListener("click", () => {
        if (this.options.newWindow) {
          window.open(this.options.destination, "_blank");
        } else {
          window.location = this.options.destination;
        }
      });
    }

    if (
      typeof this.options.onClick === "function" &&
      !this.options.destination
    ) {
      t.addEventListener("click", () => {
        this.options.onClick();
      });
    }

    if (typeof this.options.offset === "object") {
      const { x, y } = this.options.offset;
      const transform = `translate(${i("x", this.options)}, ${i("y", this.options)})`;
      t.style.transform = transform;
    }

    return t;
  }

  showToast() {
    this.toastElement = this.buildToast();

    const rootElement =
      this.options.selector &&
      document.getElementById(this.options.selector);

    if (!rootElement) {
      throw new Error("Root element is not defined");
    }

    rootElement.insertBefore(
      this.toastElement,
      rootElement.firstChild
