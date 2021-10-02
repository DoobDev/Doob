import mongoose, { Schema } from 'mongoose';

const reqString = {
    type: String,
    required: true,
};

const welcomeSchema = new Schema({
    _id: reqString, // guild id
    channelId: reqString,
    text: reqString,
});

const name = 'welcome-channels';

export default mongoose.models[name] || mongoose.model(name, welcomeSchema, name);
