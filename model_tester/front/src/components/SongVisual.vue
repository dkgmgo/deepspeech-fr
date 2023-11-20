<template>
    <div>
        <div ref="waveform" id="waveform"></div>
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
            this.wavesurfer.setHeight(350)
        },
    },
};
</script>

<style scoped>
#waveform {
    width: 100%;
    padding-top: 130px;
}
</style>
