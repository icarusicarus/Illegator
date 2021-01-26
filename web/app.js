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

const { sequelize } = require('./models');

app.set("port", process.env.PORT || 3000);
app.set("views", "./views");
app.engine('html', require('ejs').renderFile);
app.set("view engine", "html");

app.use(
  expressSession({
    secret: "illegator",
    resave: false,
    saveUninitialized: true,
    cookie: {
      maxAge: 60000 * 60,
    },
  })
);

sequelize.sync({ force: false })
  .then(() => {
    console.log("[Success] Database Connect");
  })
  .catch((err) => {
    console.error(err);
  });

var mainRouter = require("./routes/main");
var adminRouter = require("./routes/admin");
var loginRouter = require("./routes/login");
var logoutRouter = require("./routes/logout");
var registerRouter = require("./routes/register");
var findAccountRouter = require("./routes/findAccount");

app.use(logger("dev"));
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());

app.use("/", loginRouter);
app.use("/admin", adminRouter);
app.use("/main", mainRouter);
app.use("/logout", logoutRouter);
app.use("/register", registerRouter);
app.use("/findAccount", findAccountRouter);

app.use(function (req, res, next) {
  res.status(400).send("Not Found");
});

app.listen(app.get("port"), function () {
  console.log("[Listening] localhost @", app.get("port"));
});
