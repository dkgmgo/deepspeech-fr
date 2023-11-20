<template>
    <div>
        <div ref="waveform"></div>
    </div>
</template>

<script>
import WaveSurfer from "wavesurfer.js";

export default {
    data() {
        return {
            wavesurfer: null,
        };
    },
    props: {
        audioBlob: Blob,
    },
    mounted() {
        this.initializeAudio();
    },
    methods: {
        initializeAudio() {
            this.wavesurfer = WaveSurfer.create({
                container: this.$refs.waveform,
                waveColor: 'violet',
                progressColor: 'purple',
                backend: 'MediaElement',
                mediaType: 'blob',
                // TODO
                /* plugins: [
                    WaveSurfer.spectrogram.create({
                        wavesurfer: this.wavesurfer,
                        container: "#wave-spectrogram",
                        labels: true,
                        height: 256,
                    })
                ] */
            });

            this.wavesurfer.loadBlob(this.audioBlob);
        },
    },
};
</script>

<style scoped>
#waveform {
    width: 100%;
    height: 150px;
}
</style>
