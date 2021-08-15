module.exports = {
    name: 'CHICKEN', // The name of the keyword to react to,
    aliases: ['Chicken', 'chicken'], // Other keywords to react to
    message: '', // The message we're responding with
    // We could respond with text, or any other type of file instead.
    execute(message) {

        var chickenLinks = [
            'https://static.wikia.nocookie.net/minecraft_gamepedia/images/6/66/Cooked_Chicken_JE3_BE3.png',
            'https://static.wikia.nocookie.net/minecraft-earth/images/5/58/Chicken-0.png',
            'https://media.healthyfood.com/wp-content/uploads/2017/04/Bought-vs-homemade-iStock-510440285-v2-500x750.jpg',
            'https://purewows3.imgix.net/images/articles/2020_09/how-long-can-cooked-chicken-stay-in-the-fridge.jpg',
            'https://addapinch.com/wp-content/uploads/2020/03/easy-baked-chicken-breast-recipe-addapinch-1018.jpg',
            'https://media.istockphoto.com/photos/grilled-chicken-picture-id172900971?k=6&m=172900971&s=612x612&w=0&h=AtjTWJhp8elweWDETJFYG2Mp2liEB0zgMaNaopgisnY='
        ];



        return message.channel.send(chickenLinks[Math.floor(Math.random() * chickenLinks.length)]);
    },
};