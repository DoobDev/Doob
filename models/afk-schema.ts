import mongoose, { Schema } from 'mongoose';

const reqString = {
    type: String,
    required: true,
};

const afkSchema = new Schema({
    _id: reqString, // User ID
    message: { type: String, required: false },
    time: reqString,
});

const name = 'afk-users';

export default mongoose.models[name] || mongoose.model(name, afkSchema, name);
