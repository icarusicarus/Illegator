const express = require("express");
const crypto = require("crypto");
const nodemailer = require("nodemailer");
const router = express.Router();
const { User } = require('../models');

router.route('/')
    .get(async (req, res, next) => {
        res.render("findAccount.html");
    })

router.route('/findId')                          // find by email. if email is correct, show id
    .post(async (req, res, next) => {
        console.log("[POST] Find ID");
        const findId = await User.findOne({
            attributes: ['username'],
            where: {
                email: req.body.email
            }
        }, { raw: true });

        if (findId != null) {
            res.json({ id: findId.username });
        } else {
            res.json({ error: 'no such user' });
        }
    })

router.route('/findPw')                         // send email and update database
    .post(async (req, res, next) => {
        const findPw = await User.findOne({
            where: {
                username: req.body.id,
                email: req.body.email
            }
        }, { raw: true });

        // check valid account
        if (findPw != null) {
            // create new password and salt
            var pw = '';
            const char = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
            for (var i = 0; i < 20; i++) {
                pw += char.charAt(Math.floor(Math.random() * char.length));
            }
            const salt = crypto.randomBytes(64).toString("base64");
            var hashPw = crypto
                .pbkdf2Sync(pw, salt, 100, 64, "sha512")
                .toString("base64");

            // update DB
            console.log("New info: " + pw + "/" + salt);
            console.log("try to update db");
            console.log(req.body);
            User.update({
                password: hashPw,
                salt: salt,
            }, {
                where: {
                    username: req.body.id,
                    email: req.body.email
                }
            });
            console.log("DB update success");

            // send email
            let transporter = nodemailer.createTransport({
                service: 'gamil',
                host: 'smtp.gmail.com',
                secure: false,
                auth: {
                    user: '0flame0dawn0@gmail.com',
                    pass: 'filterd',
                },
            });

            let info = await transporter.sendMail({
                from: '"Icarus🐍" <0flame0dawn0@gmail.com>',
                to: req.body.email,
                subject: 'Password Change Mail👋',
                html: `<b>Test email</b><br><div><label>new password: </label>${pw}</div>`,
            });

            console.log('Message sent: %s', info.messageId);
            res.redirect('/');


        } else {
            res.json({ error: 'no such user' });
        }

    })



module.exports = router;
