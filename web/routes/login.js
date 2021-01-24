const express = require("express");
const fs = require("fs");
const crypto = require("crypto");
const router = express.Router();
const User = require("../models/user")

var loginPage = function (req, res, alert) {
    res.render("login.ejs", {
        msg: alert,
    });
};

router.route('/')
    .get(async (req, res, next) => {
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
    })
    .post(async (req, res, next) => {
        console.log("Login POST!!!!");
        const id = req.body.username;
        const pw = req.body.password;
        console.log(req.body);

        if (id && pw) {
            const hashPW = getHashPW(id, pw);
            if (!hashPw) {
                console.log("Login fail, redirect login page");
                loginPage(req, res, "No such user! You need to register.");
            } else {
                try {
                    const login = await User.findAll({
                        where: {
                            username: id,
                            password: hashPw
                        }
                    });
                    console.log("Login?: " + login);
                    if (login) {

                        req.session.loggedin = true;
                        req.session.uid = id;
                        res.redirect("/");
                    }
                } catch (err) {
                    console.error(err);
                    loginPage(req, res, "No such user! You need to register.");
                }
            }
        }
    })


function getHashPW(username, pw, callback) {
    console.log("Username: " + username);

    const salt = User.findAll({
        attributes: ['salt'],
        where: {
            username: username
        }
    });
    console.log("Salt: " + salt[0]);


    if (salt) {
        const hashPw = crypto
            .pbkdf2Sync(pw, salt, 100, 64, "sha512")
            .toString("base64");
    } else {
        console.log("[Error] getHashPW: Can't find correspond ID.");
        return 0;
    }

    return hashPw;
}

module.exports = router;
