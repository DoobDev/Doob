import mongoose, { Schema } from 'mongoose';

const reqString = {
    type: String,
    required: true,
};

const loggingSchema = new Schema({
    _id: reqString, // Guild ID
    channelId: reqString,
});

const name = 'logging-channels';

export default mongoose.models[name] || mongoose.model(name, loggingSchema, name);
