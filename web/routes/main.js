const express = require('express');
const router = express.Router();

router.get('/', function (req, res) {
    console.log("[Main POST] Main page loading...");
    if (req.session.loggedin) {
        if (req.session.uid == "admin") {
            res.redirect('admin');
        } else {
            res.render('main');
        }
    } else {
        res.redirect('/');
    }
});

module.exports = router;