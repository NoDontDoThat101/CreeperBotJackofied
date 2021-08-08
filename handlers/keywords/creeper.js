/**
 * This class responds to anyone that types "creeper" or any of the aliases listed below with the gif defined below.
 */
module.exports = {
    name: 'CREEPER', // The name of the keyword to react to,
    aliases: ['Creeper', 'creeper'], // Other keywords to react to
    message: 'aw man', // The message we're responding with
    // We could respond with text, or any other type of file instead.
    execute(message) {
        return message.channel.send(this.message);
    },
};