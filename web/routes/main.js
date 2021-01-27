const express = require('express');
const { User } = require('../models');
const router = express.Router();

router.get('/', async function (req, res) {
    console.log("[Main POST] Main page loading...");
    if (req.session.loggedin) {
        if (req.session.uid == "admin") {
            res.redirect('admin');
        } else {
            res.render('main', { uid: req.session.uid });
            console.log("Permisson OK!");
        }
    } else {
        res.redirect('/');
    }
});

module.exports = router;