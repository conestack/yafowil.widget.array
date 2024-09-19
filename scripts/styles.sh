#!/bin/bash

SASS_BIN="./node_modules/sass/sass.js"
SASS_DIR="./scss"
TARGET_DIR="./src/yafowil/widget/array/resources"

$SASS_BIN $SASS_DIR/widget_default.scss --no-source-map $TARGET_DIR/default/widget.css
$SASS_BIN $SASS_DIR/widget_bootstrap.scss --no-source-map $TARGET_DIR/bootstrap/widget.css
$SASS_BIN $SASS_DIR/widget_plone5.scss --no-source-map $TARGET_DIR/plone5/widget.css
$SASS_BIN $SASS_DIR/widget_bootstrap5.scss --no-source-map $TARGET_DIR/bootstrap5/widget.css
