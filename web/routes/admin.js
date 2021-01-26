const express = require('express');
const { User } = require('../models');
const router = express.Router();

router.route('/')
    .get(async (req, res, next) => {
        console.log("[Admmin GET] Admin page loading...");

        var userList = new Array();

        const user = await User.findAll({
            attributes: ['username', 'email', 'permission'],
            where: {
                permission: 0
            }
        }, { raw: true });

        for (var i = 0; i < user.length; i++) {
            userList.push(user[i].dataValues);
        }

        var jsonData = JSON.stringify(userList);

        res.render('admin.ejs', { 'userList': jsonData });
    })

router.route('/permit')
    .post(async (req, res, next) => {
        await User.update({ permission: 1 }, {
            where: {
                username: req.body.username,
                email: req.body.email
            }
        });
    })

module.exports = router;