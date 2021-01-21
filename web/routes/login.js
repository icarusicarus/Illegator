const express = require("express");
const mysql = require("mysql");
const fs = require("fs");
const crypto = require("crypto");
const router = express.Router();

var conn = mysql.createConnection({
    host: "localhost",
    user: "illegator",
    password: "!11eGAt0R",
    database: "users",
});

conn.connect();

var loginPage = function (req, res, alert) {
    res.render("login.ejs", {
        msg: alert,
    });
};

router.get("/", function (req, res) {
    var uid = req.session.uid;
    console.log(uid);
    if (uid == undefined) {
        console.log("[Login GET] Login page loading...");
        loginPage(req, res);
    } else {
        console.log("[Login GET] Already loggedin. Go to main page.");
        res.render("main.ejs", {
            uid: uid,
        });
    }
});

router.post("/", function (req, res) {
    const id = req.body.username;
    const pw = req.body.password;
    console.log(req.body);

    if (id && pw) {
        getHashPW(id, pw, (error, hashPw) => {
            if (error || hashPw == null) {
                console.log("[Login GET] Success: Loin page loading...");
                loginPage(req, res, "No such user! You need to register.");
            } else {
                console.log("HashPW: " + hashPw);
                conn.query(
                    "SELECT * FROM `users`.`user` WHERE username=? AND password=?",
                    [id, hashPw],
                    (error, result) => {
                        console.log("[Login POST] SQL Log: " + this.sql);
                        if (result.length > 0) {
                            req.session.loggedin = true;
                            req.session.uid = id;
                            res.redirect("/");
                        } else {
                            loginPage(req, res, "No such user! You need to register.");
                        }
                        res.end();
                    }
                );
            }
        });
    } else {
        loginPage(req, res, "Please enter ID and Password correctly.");
    }
});

function getHashPW(username, pw, callback) {
    console.log(username);
    conn.query(
        "SELECT salt FROM `users`.`user` WHERE username=?",
        [username],
        (error, result) => {
            if (error) {
                console.log("[Error] getHashPW: " + error);
                callback(error, null);
            } else {
                if (result.length > 0) {
                    const hashPw = crypto
                        .pbkdf2Sync(pw, result[0].salt, 100, 64, "sha512")
                        .toString("base64");
                    callback(error, hashPw);
                } else {
                    console.log("[Error] getHashPW: Can't find correspond ID.");
                    callback(error, null);
                }
            }
        }
    );
}

module.exports = router;
