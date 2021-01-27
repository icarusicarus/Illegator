var express = require('express');
var fs = require('fs');
const crypto = require("crypto");
const { User } = require('../models');
var router = express.Router();
var path = require('path');

/*
var registerPage = function (req, res, alert) {
    res.render('register.html', {
        msg: alert
    })
}

var loginPage = function (req, res, alert) {
    res.render('login.html', {
        msg: alert
    })
}
*/

var registerPage = function (req, res, alert) {
    res.sendFile(path.resolve('./views/register.html'));
    
}

var loginPage = function (req, res, alert) {
    res.sendFile(path.resolve('./views/login.html'));
};


router.route('/')
    .get(async (req, res, next) => {
        console.log('[Ragister GET] Register page loading...');
        registerPage(req, res);
    })
    .post(async (req, res, next) => {
        try {
            var id = req.body.id;
            var pw = req.body.pw;
            var email = req.body.email;

            console.log("Try to add user");
            var salt = crypto.randomBytes(64).toString("base64");
            var hashPw = crypto
                .pbkdf2Sync(req.body.pw, salt, 100, 64, "sha512")
                .toString("base64");
            console.log(hashPw);

            const addUser = await User.create({
                username: id,
                password: hashPw,
                salt: salt,
                email: email,
                permission: 0,
            });

            console.log(addUser);
            console.log("Success to INSERT new user");
            loginPage(req, res, "Register success. Try login!");
        } catch (err) {
            console.log("Failed to INSERT new user");
            registerPage(req, res, "Register failed, DB error");
        }
    })

router.route('/idcheck')
    .post(async (req, res, next) => {
        console.log("[POST] ID Check");
        const idcheck = await User.findOne({
            where: {
                username: req.body.id
            }
        }, { raw: true });

        if (idcheck != null) {
            res.json({ duplicate: 1 });
            console.log("ID Dup");
        } else {
            res.json({ duplicate: 0 });
            console.log("ID OK");
        }
    })

module.exports = router;

