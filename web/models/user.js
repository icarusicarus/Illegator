//models/user.js
const Sequelize = require('sequelize');

module.exports = class User extends Sequelize.Model {
    static init(sequelize) {
        return super.init({
            username: {
                type: Sequelize.STRING(20),
                allowNull: false,
            },
            password: {
                type: Sequelize.STRING(100),
                allowNull: false,
            },
            salt: {
                type: Sequelize.STRING(100),
                allowNull: false,
            },
            permission: {
                type: Sequelize.BOOLEAN,
                allowNull: true,
            },
            email: {
                type: Sequelize.STRING(100),
                allowNull: false,
            },
        }, {
            sequelize,
            timestamps: false,
            underscored: false,
            modelName: 'User',
            tableName: 'users',
            paranoid: false,
            charset: 'utf8',
            collate: 'utf8_general_ci',
        });
    }
};
