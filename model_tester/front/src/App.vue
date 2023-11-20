<template>
  <v-app>
    <v-main>
      <v-card flat>
        <v-tabs
          v-model="tab"
          background-color="deep-purple accent-4"
          centered
          dark
          icons-and-text
        >
          <v-tabs-slider></v-tabs-slider>

          <v-tab href="#tab-1">
            Model Tester
            <v-icon>mdi-test-tube</v-icon>
          </v-tab>

          <v-tab href="#tab-2">
            ChatBot
            <v-icon>mdi-message</v-icon>
          </v-tab>
        </v-tabs>

        <v-tabs-items v-model="tab">
          <v-tab-item value="tab-1">
            <v-card flat>
              <v-card-text>
                <ModelTesterTab/>
              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item value="tab-2">
              <v-card flat>
                <v-card-text>
                  <ChatbotTab/>
                </v-card-text>
              </v-card>
            </v-tab-item>
        </v-tabs-items>
      </v-card>
    </v-main>
  </v-app>
</template>

<script>
import ModelTesterTab from "@/components/ModelTesterTab.vue";
import ChatbotTab from "./components/ChatbotTab.vue";

export default {
  name: 'App',

  components: {
    ModelTesterTab,
    ChatbotTab
},

  data() {
    return {
      tab: null,
    }
  },
};
</script>
