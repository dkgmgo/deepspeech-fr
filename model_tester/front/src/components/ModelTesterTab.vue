<template>
    <v-container>
        <v-row class="text-center">
            <v-col>
                <p class="text-h6">Pour commencer, veuillez sélectionner un modèle parmi ceux disponibles.</p>
                <v-radio-group v-model="selectedModel">
                    <v-radio v-for="el in models" :key=el :label=el :value=el @click="loadModel(el)"></v-radio>
                </v-radio-group>
            </v-col>
        </v-row>

        <v-row class="text-center">
            <v-col>
                <v-btn @click="startRecording"  class="light-green" v-if="!isRecording">
                    Enregistrer
                    <v-icon right dark>mdi-microphone</v-icon>
                </v-btn>
                <v-btn @click="stopRecording" color="red" v-if="isRecording">
                    Arrêter
                    <v-icon right dark>mdi-microphone</v-icon>
                </v-btn>
            </v-col>
            <v-col v-if="!isRecording && audioBlob">
                <v-row>
                    <v-col><v-btn class="teal" @click="sendAudio">
                        Reconnaître
                        <v-icon right dark>mdi-cloud-upload</v-icon>
                    </v-btn></v-col>
                </v-row>
                <v-row>
                    <v-col><audio :src="audioUrl" controls></audio></v-col>
                </v-row>
            </v-col>
        </v-row>

        <v-row>
            <v-col v-if="!isRecording && audioBlob">
                <SongVisual :audioBlob="audioBlob"/>
            </v-col>
        </v-row>

        <v-row class="text-center">
            <v-col>
                <v-progress-circular v-if="loader" color="deep-purple accent-4" indeterminate :size="120" :width="11"></v-progress-circular>
                <br>
                <p class="text-huge" v-text="prediction"></p>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import api from '@/api.js';
import vmsg from 'vmsg'
import SongVisual from './SongVisual.vue';

export default{
    name: "ModelTesterTab",

    components: {
        SongVisual
    },

    data(){
        return {
            models: [],
            selectedModel: "",
            isRecording: false,
            mediaRecorder: null,
            audioBlob: null,
            prediction: "",
            audioSent: false
        }
    },

    async mounted(){
        this.models = await api.listModels()
        api.loadModel("")
        this.mediaRecorder = new vmsg.Recorder({
            wasmURL: "https://unpkg.com/vmsg@0.3.0/vmsg.wasm"
        });
    },

    computed: {
        audioUrl(){
            return this.audioBlob ? URL.createObjectURL(this.audioBlob) : "" 
        },

        loader(){
            return this.audioSent && !this.prediction
        }
    },

    methods: {

        loadModel(model){
            api.loadModel(model)
        },

        async startRecording() {
            try {
                await this.mediaRecorder.initAudio();
                await this.mediaRecorder.initWorker();
                this.mediaRecorder.startRecording();
                this.isRecording = true
            } catch (e) {
                console.error(e);
            }
        },

        async stopRecording() {
            if(this.isRecording){
                this.audioBlob = await this.mediaRecorder.stopRecording()
                this.isRecording = false
            }
        },

        async sendAudio() {
            if (this.audioBlob) {
                this.audioSent = true
                this.prediction = ""
                const formData = new FormData();
                formData.append('audio', this.audioBlob, 'audio.mp3');
                this.prediction = await api.recognizeMp3(formData)
            }
        },
    },
}
</script>

<style scoped>
.text-center {
    text-align: center;
}

.text-huge {
    font-size: 3em;
    font-weight: bold;
}
</style>