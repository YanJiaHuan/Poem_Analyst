<template>
  <v-app>
    <!--姓名 抬头-->
    <v-card
      class="fixCard"
    >
      <v-toolbar color=#f3f7e4 shaped>
        <v-toolbar-title>{{ "\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0" }}Hello {{nameID}}  ^^</v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
      <v-banner single-line :sticky="sticky">
        This is the feedback.
      </v-banner>
      <!-- <v-card-text class="grey lighten-4">
        <v-sheet class="mx-auto"></v-sheet>
      </v-card-text> -->
    </v-card>
    <h1><br><br><br></h1>
    <!-- 附加 -->
    <v-container
      class="try"
    >
    <v-container
      style="max-width: 620px"
    >
      <v-divider class="mt-4"></v-divider>
      <v-row
        class="my-4"
        align="center"
      >
        <strong class="mx-5 info--text text--darken-3">
          Please score the Translation:
        </strong>
        <!-- <v-spacer></v-spacer>
        <v-progress-circular
          :value="progress"
          class="mr-2"
        ></v-progress-circular> -->
      </v-row>
      <v-divider class="mt-1"></v-divider>
      <!-- <v-row
        class="my-1"
        align="center"
      >
        <strong class="mx-6 info--text text--darken-2">
          Remaining: {{ remainingTasks }}
        </strong>
        <v-divider vertical></v-divider>
        <strong class="mx-6 success--text text--darken-2">
          Completed: {{ completedTasks }}
        </strong>
      </v-row> -->
      <v-divider class="mb-2"></v-divider>
      <v-card v-if="tasks.length > 0">
        <v-slide-y-transition
          class="py-0"
          group
          tag="v-list"
        >
          <template v-for="(task, i) in tasks">
            <v-divider
              v-if="i !== 0"
              :key="`${i}-divider`"
            ></v-divider>
            <v-list-item :key="`${i}-${task.text}`">
              <v-list-item-action>
                <v-checkbox
                  v-model="task.done"
                  :color="task.done && 'grey' || 'primary'"
                >
                  <template v-slot:label>
                    <div
                      :class="task.done && 'grey--text' || 'primary--text'"
                      class="ml-4"
                      v-text="task.text"
                    ></div>
                  </template>
                </v-checkbox>
              </v-list-item-action>
              <v-spacer></v-spacer>
              <v-scroll-x-transition>
                <v-icon
                  v-if="task.done"
                  color="success"
                >
                  mdi-check
                </v-icon>
              </v-scroll-x-transition>
            </v-list-item>
          </template>
        </v-slide-y-transition>
      </v-card>
    </v-container>
    </v-container>

    <div>
      <h2><br></h2>
          <!--返回主页-->
        <v-hover
          v-slot="{ hover }"
          open-delay="10">
          <v-btn
            :elevation="hover ? 10 : 2"
            :class="{ 'on-hover': hover }"
            color= #82A5D2
            x-large
            v-on:click="submit">Back to main page{{ "\xa0" }}
            <v-icon color="blue-grey darken-3" large>mdi-home</v-icon>
          </v-btn>
        </v-hover>
      <h2><br><br><br></h2>
      <h4>Copyright ©️ 2023 Lucky7</h4>
    </div>
  </v-app>
</template>
<script>

export default {
  name: 'Feedback',
  components: {},
  data() {
    return {
      nameID: '',
      tasks: [
        {done: false, text: 'Very satisfied  ;-)'},
        {done: false, text: 'More satisfied  :-)'},
        {done: false, text: 'General satisfied  :-|'},
        {done: false, text: 'Less satisfied  :-('},
        {done: false, text: 'Not satisfied  ;-('}
      ],
      backTopShow: false,
      newTask: null
    }
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll)
  },
  created() {
    this.nameID = this.$route.params.nameID
  },
  computed: {
    completedTasks () {
      return this.tasks.filter(task => task.done).length
    },
    progress () {
      return this.completedTasks / this.tasks.length * 100
    },
    remainingTasks () {
      return this.tasks.length - this.completedTasks
    }
  },
  methods: {
    handleScroll() {
      if (document.documentElement.scrollTop + document.body.scrollTop > 500) {
        this.backTopShow = true
      } else {
        this.backTopShow = false
      }
    },
    create () {
      this.tasks.push({
        done: false,
        text: this.newTask
      })
      this.newTask = null
    },
    submit() {
      // 跳转到下一页
      this.$router.push(
        {
          path: '/',
          name: 'HelloWorld',
          params: {
            nameID: this.nameID
          }
        })
    }
  }
}
</script>

<style scoped>
h4 {
  font-weight: normal;
  color: #818181;
}
.goTop {
  position: fixed;
  z-index: 999999;
  right: 50px;
  bottom: 8%;
}
.rightCard {
  width: 27%;
  right: 20px;
  top: 17%;
}
.fixCard {
  z-index: 999999;
  position: fixed;
  width: 100%;
}
.try {
  top: 5%;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>
