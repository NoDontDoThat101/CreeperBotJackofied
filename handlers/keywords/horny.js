/**
 * This class responds to anyone that types "creeper" or any of the aliases listed below with the gif defined below.
 */
module.exports = {
    name: 'how\'s creeper bot', // The name of the keyword to react to,
    aliases: ['How is creeper bot?', 'how is creeper bot?', 'how is creeper bot', 'How is creeper bot', 'How\'s creeper bot', 'how\'s creeper bot?', 'How\'s creeper bot?'], // Other keywords to react to
    message: 'Horny', // The message we're responding with
    // We could respond with text, or any other type of file instead.
    execute(message) {
        return message.channel.send(this.message);
    },
};