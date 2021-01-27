const express = require('express');
const { User } = require('../models');
const router = express.Router();

router.route('/')
    .get(async (req, res, next) => {

        if (req.session.uid == 'admin') {
            console.log("[Admmin GET] Admin page loading...");
            var userList = new Array();

            const user = await User.findAll({
                attributes: ['username', 'email', 'permission'],
                where: {
                    permission: 0
                }
            }, { raw: true });

            res.render('admin.html', { 'userList': user });
        } else {
            console.log("[WARNING] You are not ADMIN");
            res.redirect("main");
        }
    })

router.route('/permit')
    .post(async (req, res, next) => {
        console.log(req.body);
        await User.update({ permission: 1 }, {
            where: {
                username: req.body['username'],
                email: req.body['email']
            }
        });
        res.redirect('/admin');
    })

module.exports = router;
