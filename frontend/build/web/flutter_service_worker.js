'use strict';
const MANIFEST = 'flutter-app-manifest';
const TEMP = 'flutter-temp-cache';
const CACHE_NAME = 'flutter-app-cache';

const RESOURCES = {
  "version.json": "46a52461e018faa623d9196334aa3f50",
  "index.html": "cc1a3ce1e56133270358b49a5df3f0bf",
  "main.dart.js": "e2161c7a27249ead50512890f62bd1cf",
  "flutter.js": "6fef97aeca90b426343ba6c5c9dc5d4a",
  "favicon.png": "5dcef449791fa27946b3d35ad8803796",
  "icons/Icon-192.png": "ac9a721a12bbc803b44f645561ecb1e1",
  "icons/Icon-maskable-192.png": "c457ef57daa1d16f64b27b786ec2ea3c",
  "icons/Icon-maskable-512.png": "301a7604d45b3e739efc881eb04896ea",
  "icons/Icon-512.png": "96e752610906ba2a93c65f8abe1645f1",
  "manifest.json": "0fa552613b8ec0fda5cda565914e3b16",
  "assets/AssetManifest.json": "1b1e4a4276722b65eb1ef765e2991840",
  "assets/NOTICES": "28ba0c63fc6e4d1ef829af7441e27f78",
  "assets/FontManifest.json": "dc3d03800ccca4601324923c0b1d6d57",
  "assets/packages/cupertino_icons/assets/CupertinoIcons.ttf": "055d9e87e4a40dbf72b2af1a20865d57",
  "assets/packages/fluttertoast/assets/toastify.js": "56e2c9cedd97f10e7e5f1cebd85d53e3",
  "assets/packages/fluttertoast/assets/toastify.css": "a85675050054f179444bc5ad70ffc635",
  "assets/shaders/ink_sparkle.frag": "f8b80e740d33eb157090be4e995febdf",
  "assets/AssetManifest.bin": "791447d17744ac2ade3999c1672fdbe8",
  "assets/fonts/MaterialIcons-Regular.otf": "245e0462249d95ad589a087f1c9f58e1",
  "assets/assets/tree_structure.json": "cda9b1a239f956c547411efad9f7c794",
  "assets/assets/google_logo.svg.png": "0e29f8e1acfb8996437dbb2b0f591f19",
  "assets/assets/images/discord_logo.png": "0e4a4162c5de8665a7d63ae9665405ae",
  "assets/assets/images/google_logo.svg.png": "0e29f8e1acfb8996437dbb2b0f591f19",
  "assets/assets/images/github_logo.svg.png": "ba087b073efdc4996b035d3a12bad0e4",
  "assets/assets/images/twitter_logo.png": "af6c11b96a5e732b8dfda86a2351ecab",
  "assets/assets/images/autogpt_logo.png": "6a5362a7d1f2f840e43ee259e733476c",
  "assets/assets/github_logo.svg.png": "ba087b073efdc4996b035d3a12bad0e4",
  "assets/assets/coding_tree_
