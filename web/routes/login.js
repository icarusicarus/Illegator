const express = require("express");
const fs = require("fs");
const crypto = require("crypto");
const router = express.Router();
const { User } = require('../models');

var loginPage = function (req, res, alert) {
    res.render("login.html", {
        msg: alert,
    });
};

router.route('/')
    .get(async (req, res, next) => {
        console.log(req.session.loggedin);
        if (req.session.loggedin == undefined) {
            console.log("[Login GET] Login page loading...");
            loginPage(req, res);
        } else {
            console.log("[Login GET] Already loggedin. Go to main page.");
            res.redirect("main");
        }
    })
    .post(async (req, res, next) => {
        console.log("[Login POST]");
        const id = req.body.username;
        const pw = req.body.password;

        if (id && pw) {
            const hashPW = await getHashPW(id, pw);
            if (!hashPw) {
                console.log("Login fail, redirect login page");
                loginPage(req, res, "No such user! You need to register.");
            } else {
                try {
                    const login = await User.findOne({
                        where: {
                            username: id,
                            password: hashPw
                        }
                    }, { raw: true });

                    var logged = login.username;
                    if (logged) {
                        if (login.permission == 0) {
                            res.render('login', { msg: "permission denied" });
                            console.log("Permisson Denied");
                        } else {
                            req.session.loggedin = true;
                            req.session.uid = id;
                            res.redirect('/main');
                            console.log("Permisson OK!");
                        }
                    }
                } catch (err) {
                    console.error(err);
                    loginPage(req, res, "No such user! You need to register.");
                }
            }
        }
    })


async function getHashPW(username, pw, callback) {
    const result = await User.findAll({
        attributes: ['salt'],
        where: { username: username }
    }, { raw: true });

    var salt = result[0].salt;
    var hashPW;
    if (salt) {
        hashPw = crypto
            .pbkdf2Sync(pw, salt, 100, 64, "sha512")
            .toString("base64");
    } else {
        console.log("[Error] getHashPW: Can't find correspond ID.");
        return 0;
    }
    return hashPw;
}

module.exports = router;
