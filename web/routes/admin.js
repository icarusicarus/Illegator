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
    .post(async (req, res, next) => {
        //
    })

module.exports = router;

// get 에서 데이터 받아서 뿌려줘야하는데 데이터를 어떻게 받아올지 몰라서 찾아보는 중임