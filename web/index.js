var createError = require("http-errors");
var express = require("express");
var path = require("path");
var cookieParser = require("cookie-parser");
var logger = require("morgan");
var bodyParser = require("body-parser");
var expressErrorHandler = require("express-error-handler");
var expressSession = require("express-session");
var mysql = require("mysql");
var app = express();

app.set("port", process.env.PORT || 3000);
app.set("views", "./views");
app.set("view engine", "ejs");

var mainRouter = require("./routes/main");

app.use(logger("dev"));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());

app.use("/", mainRouter);

app.use(function (req, res, next) {
    res.status(400).send("Not Found");
  });
  
  app.listen(app.get("port"), function () {
    console.log("[Listening] localhost @", app.get("port"));
  });
  