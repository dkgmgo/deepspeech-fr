import axios from 'axios';


const baseUrl = "http://localhost:8000/";
const instanceAxios = axios.create(
    {
        baseURL: baseUrl,
        crossdomain: true,
    }
)


const recognizeMp3 = async (formData) => {
    let prediction = ""

    try{
        const response = await instanceAxios.post('recognize', formData,{
        headers: {
            'Content-Type': 'multipart/form-data',
        },})
        prediction = response.data.prediction
    }catch (error) {
        console.error('Error while recognizing the audio', error);
    }

    return prediction
}

const loadModel = async (selectedModel) => {
    instanceAxios.post('load', {
        'model': selectedModel
    }).then(response => {
        console.log(response.data);
    }).catch(error => {
        console.error('Error loading the model:', error);
    })
}

const listModels = async () => {
    let list = [];

    try {
        const response = await instanceAxios.get('list');
        list = response.data;
    } catch (error) {
        console.error('Error listing the models:', error);
    }

    return list
}

const api = {"recognizeMp3": recognizeMp3, "loadModel": loadModel, "listModels": listModels}

export default api