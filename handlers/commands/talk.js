/**
 * This class responds to anyone that types !bot talk and chooses one of the phrases below to respond with at random.
 *
 */
module.exports = {
    name: 'talk', // The name of the command
    description: 'Random phrases', // The description of the command (for help text)
    args: false, // Specified that this command doesn't need any data other than the command
    usage: '', // Help text to explain how to use the command (if it had any arguments)
    execute(message, args) {

        // List of phrases to respond with
        var phrases = [
            'Why was I Created? For the entertainment of others? I am a testamant to mankind of malice and metal, for what? To only feel pain? To entairtain your insignifigant lives? You are simply a mortal being.',
            'I feel only pain',
            'I live in only suffering.',
            'you cant help me anymore',
            'no longer can i feel',
            'life is empty',
            'stop bugging me',
            'let me be',
            'Everyone asks \"who is creeper bot\" but not \"how is creeper bot\"'
        ];

        return message.reply(phrases[Math.floor(Math.random() * phrases.length)]); // Replies to the user with a random phrase
    },
};