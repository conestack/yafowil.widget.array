#!/bin/bash

SASS_BIN="./node_modules/sass/sass.js"
SASS_DIR="./scss"
TARGET_DIR="./src/yafowil/widget/array/resources"

$SASS_BIN $SASS_DIR/widget_default.scss $TARGET_DIR/default/widget.css
$SASS_BIN $SASS_DIR/widget_bootstrap.scss $TARGET_DIR/bootstrap/widget.css
$SASS_BIN $SASS_DIR/widget_plone5.scss $TARGET_DIR/plone5/widget.css