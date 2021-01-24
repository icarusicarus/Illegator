const express = require('express');
const router = express.Router();

router.post('/', function (req, res) {
    console.log("[LOGOUT]");

    if (req.session.loggedin) {
        req.session.destroy();
        res.redirect('/');
        res.end();
    }
});

module.exports = router;