<template>
  <v-app>
    <!--进度条-->
    <v-progress-linear
      color="blue-grey"
      height="25"
      :value="degree"
      striped
      fixed
      background-color=#d1d8dc
    >
    </v-progress-linear>
    <h3><br></h3>
    <!--姓名 抬头-->
    <v-card
      class="fixCard"
    >
      <v-toolbar color=#f3f7e4 shaped>
        <v-toolbar-title>{{ "\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0" }}Your xx is: {{nameID}} </v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
      <v-banner single-line :sticky="sticky">
        Please see the output.
      </v-banner>
      <!-- <v-card-text class="grey lighten-4">
        <v-sheet class="mx-auto"></v-sheet>
      </v-card-text> -->
    </v-card>

    <v-container
      class="try"
    >
      <!--问卷-->
      <v-container
        style="max-width: 690px"
        v-model='active_question'
      >
      <h1><br><br></h1>
        <!--问题1-->
        <v-container>
          <v-divider class="mt-4"></v-divider>
          <v-row
            class="my-1"
          >
            <strong class="mx-4 info--text text--darken-3">
              Question 1
            </strong>
            <v-divider vertical></v-divider>
            <strong class="mx-4 success--text text--darken-3">
              Please select your year of birth:
            </strong>
            <v-spacer></v-spacer>
          </v-row>
          <v-divider class="mb-4"></v-divider>
          <v-col offset=2>
          <v-select
            style="max-width: 510px"
            v-on:click.native="jump"
            v-model="question1"
            :items="age"
            label="Your Year of Birth"
            dense
          ></v-select>
          </v-col>
        </v-container>
        <!--问题2-->
        <v-container>
          <v-divider class="mt-0"></v-divider>
          <v-row
            class="my-1"
          >
            <strong class="mx-4 info--text text--darken-3">
              Question 2
            </strong>
            <v-divider vertical></v-divider>
            <strong class="mx-4 success--text text--darken-3">
              Please
            </strong>
            <v-spacer></v-spacer>
          </v-row>
          <v-divider class="mb-4"></v-divider>
          <v-radio-group
            v-model="question2"
            column
            class="text-subtitle-2"
          >
            <v-divider vertical></v-divider>
            <v-col offset=2>
            <v-row class="pb-1">
            <v-radio
              label="A. Developed Countries in North American"
              :value="1"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
            <v-radio
              label="B. Developed Countries in European"
              :value="2"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
            <v-radio
              label="C. Developed Countries in Oceania"
              :value="3"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
            <v-radio
              label="D. Developed Countries in Asian"
              :value="4"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
            <v-radio
              label="E. Developing Countries"
              :value="5"
              color=#4d7e6b
              v-on:click="jump"
            >
            </v-radio>
            </v-row>
            </v-col>
          </v-radio-group>
        </v-container>
        <!--问题3-->
        <v-container>
          <v-divider class="mt-0"></v-divider>
          <v-row
            class="my-1"
          >
            <strong class="mx-4 info--text text--darken-3">
              Question 3
            </strong>
            <v-divider vertical></v-divider>
            <strong class="mx-4 success--text text--darken-3">
              What type of job do you want?
            </strong>
            <v-spacer></v-spacer>
          </v-row>
          <v-divider class="mb-4"></v-divider>
          <v-radio-group
            v-model="question3"
            column
            class="text-subtitle-2"
          >
            <v-divider vertical></v-divider>
            <v-col offset=2>
            <v-row class="pb-1">
            <v-radio
              label="A. Full-time job with contract"
              :value="0"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
            <v-radio
              label="B. Part-time Job / Internship"
              :value="1"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            </v-col>
          </v-radio-group>
        </v-container>
        <!--问题4-->
        <v-container >
          <v-divider class="mt-0"></v-divider>
          <v-row
            class="my-1"
          >
            <strong class="mx-4 info--text text--darken-3">
              Question 4
            </strong>
            <v-divider vertical></v-divider>
            <strong class="mx-4 success--text text--darken-3">
              Do you want to work from home?
            </strong>
            <v-spacer></v-spacer>
          </v-row>
          <v-divider class="mb-4"></v-divider>
          <v-radio-group
            v-model="question4"
            column
            class="text-subtitle-2"
          >
            <v-divider vertical></v-divider>
            <v-col offset=2>
            <v-row class="pb-1">
            <v-radio
              label="A. Yes"
              :value="1"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
            <v-radio
              label="B. No"
              :value="0"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            </v-col>
          </v-radio-group>
        </v-container>
        <!--问题5-->
        <v-container >
          <v-divider class="mt-0"></v-divider>
          <v-row
            class="my-1"
          >
            <strong class="mx-4 info--text text--darken-3">
              Question 5
            </strong>
            <v-divider vertical></v-divider>
            <strong class="mx-4 success--text text--darken-3">
              Do you have work experience in related industries?
            </strong>
            <v-spacer></v-spacer>
          </v-row>
          <v-divider class="mb-4"></v-divider>
          <v-radio-group
            v-model="question5"
            column
            class="text-subtitle-2"
          >
            <v-divider vertical></v-divider>
            <v-col offset=2>
            <v-row class="pb-1">
            <v-radio
              label="A. Have management experience"
              :value="3"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
            <v-radio
              label="B. Have long-term work experience"
              :value="2"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
            <v-radio
              label="C. Have short-term work experience"
              :value="1"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
            <v-radio
              label="D. None"
              :value="0"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            </v-col>
          </v-radio-group>
        </v-container>
        <!--问题6-->
        <v-container >
          <v-divider class="mt-0"></v-divider>
          <v-row
            class="my-1"
          >
            <strong class="mx-4 info--text text--darken-3">
              Question 6
            </strong>
            <v-divider vertical></v-divider>
            <strong class="mx-4 success--text text--darken-3">
              What is your highest education level?
            </strong>
            <v-spacer></v-spacer>
          </v-row>
          <v-divider class="mb-4"></v-divider>
          <v-radio-group
            v-model="question6"
            column
            class="text-subtitle-2"
          >
            <v-divider vertical></v-divider>
            <v-col offset=2>
            <v-row class="pb-1">
            <v-radio
              label="A. Graduate and above"
              :value="3"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
            </v-row>
            <v-row class="pb-1">
            <v-radio
              label="B. Bachelor's Degree"
              :value="2"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
            </v-row>
            <v-row class="pb-1">
            <v-radio
              label="C. Vocational Degree"
              :value="1"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
            </v-row>
            <v-row class="pb-1">
            <v-radio
              label="D. High School and below"
              :value="0"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            </v-col>
          </v-radio-group>
        </v-container>
        <!--问题7-->
        <v-container >
          <v-divider class="mt-0"></v-divider>
          <v-row
            class="my-1"
          >
            <strong class="mx-4 info--text text--darken-3">
              Question 7
            </strong>
            <v-divider vertical></v-divider>
            <strong class="mx-4 success--text text--darken-3">
              Your major direction?
            </strong>
            <v-spacer></v-spacer>
          </v-row>
          <v-divider class="mb-4"></v-divider>
          <v-radio-group
            v-model="question7"
            row
            class="text-subtitle-2"
          >
            <v-col offset=2>
            <v-row class="pb-1">
            <v-radio
              label="A. Management"
              :value="0"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
            <v-radio
              label="B. Engineering"
              :value="1"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
            <v-radio
              label="C. Law"
              :value="2"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
            <v-radio
              label="D. Art"
              :value="3"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
            <v-radio
              label="E. Service"
              :value="4"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
            <v-radio
              label="F. Economics"
              :value="5"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            </v-col>
            <v-col>
            <v-row class="pb-1">
            <v-radio
              label="G. Science"
              :value="6"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
            <v-radio
              label="H. Communication"
              :value="7"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
             <v-radio
              label="I. Medicine"
              :value="8"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
            <v-radio
              label="J. Education"
              :value="9"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
            <v-radio
              :value="10"
              color=#4d7e6b
              v-on:click="jump"
            >
            <template v-slot:label>
              <div>
                <row class="mb-4">
                K. Language{{"\xa0&\xa0"}}Literature
                </row>
              </div>
            </template>
            </v-radio>
            </v-row>
            <v-row class="pb-1">
            <v-radio
              label="L. Others"
              :value="11"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            </v-col>
          </v-radio-group>
        </v-container>
        <!--问题8-->
        <v-container >
          <v-divider class="mt-0"></v-divider>
          <v-row
            class="my-1"
          >
            <strong class="mx-4 info--text text--darken-3">
              Question 8
            </strong>
            <v-divider vertical></v-divider>
            <strong class="mx-4 success--text text--darken-3 text-left">
              Do you prefer to deal with people rather than<br> process information?
            </strong>
            <v-spacer></v-spacer>
          </v-row>
          <v-divider class="mb-4"></v-divider>
          <v-radio-group
            v-model="question8"
            column
            class="text-subtitle-2"
          >
            <v-divider vertical></v-divider>
            <v-col offset=2>
            <v-row class="pb-1">
            <v-radio
              label="A. Yes"
              value="E"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
            <v-radio
              label="B. No"
              value="I"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
            <v-radio
              label="C. Both are similar"
              value="X"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            </v-col>
          </v-radio-group>
        </v-container>
        <!--问题9-->
        <v-container >
          <v-divider class="mt-0"></v-divider>
          <v-row
            class="my-1"
          >
            <strong class="mx-4 info--text text--darken-3">
              Question 9
            </strong>
            <v-divider vertical></v-divider>
            <strong class="mx-4 success--text text--darken-3 text-left">
              Do you prefer to experience joy in real life rather than<br> being immersed in an imaginary world?
            </strong>
            <v-spacer></v-spacer>
          </v-row>
          <v-divider class="mb-4"></v-divider>
          <v-radio-group
            v-model="question9"
            column
            class="text-subtitle-2"
          >
            <v-divider vertical></v-divider>
            <v-col offset=2>
            <v-row class="pb-1">
            <v-radio
              label="A. Yes"
              value="S"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
            <v-radio
              label="B. No"
              value="N"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
            <v-radio
              label="C. Both are similar"
              value="X"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            </v-col>
          </v-radio-group>
        </v-container>
        <!--问题10-->
        <v-container >
          <v-divider class="mt-0"></v-divider>
          <v-row
            class="my-1"
          >
            <strong class="mx-4 info--text text--darken-3">
              Question 10
            </strong>
            <v-divider vertical></v-divider>
            <strong class="mx-4 success--text text--darken-3 text-left">
              Do you usually measure things by emotional value<br> rather than practical value in life?
            </strong>
            <v-spacer></v-spacer>
          </v-row>
          <v-divider class="mb-4"></v-divider>
          <v-radio-group
            v-model="question10"
            column
            class="text-subtitle-2"
          >
            <v-divider vertical></v-divider>
            <v-col offset=2>
            <v-row class="pb-1">
            <v-radio
              label="A. Yes"
              value="F"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
            <v-radio
              label="B. No"
              value="T"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
            <v-radio
              label="C. Both are similar"
              value="X"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            </v-col>
          </v-radio-group>
        </v-container>
        <!--问题11-->
        <v-container >
          <v-divider class="mt-0"></v-divider>
          <v-row
            class="my-1"
          >
            <strong class="mx-4 info--text text--darken-3">
              Question 11
            </strong>
            <v-divider vertical></v-divider>
            <strong class="mx-4 success--text text--darken-3 text-left">
              Do you want to have good social values<br> more than unique personalities?
            </strong>
            <v-spacer></v-spacer>
          </v-row>
          <v-divider class="mb-4"></v-divider>
          <v-radio-group
            v-model="question11"
            column
            class="text-subtitle-2"
          >
            <v-divider vertical></v-divider>
            <v-col offset=2>
            <v-row class="pb-1">
            <v-radio
              label="A. Yes"
              value="J"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
            <v-radio
              label="B. No"
              value="P"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            <v-row class="pb-1">
            <v-radio
              label="C. Both are similar"
              value="X"
              color=#4d7e6b
              v-on:click="jump"
            ></v-radio>
            </v-row>
            </v-col>
          </v-radio-group>
        </v-container>
      </v-container>

      <!-- 附加
      <v-container
        style="max-width: 320px"
      >
        <v-divider class="mt-4"></v-divider>
        <v-row
          class="my-1"
          align="center"
        >
          <strong class="mx-5 info--text text--darken-6">
            Check Bar
          </strong>
          <v-spacer></v-spacer>
          <v-progress-circular
            :value="progress"
            class="mr-2"
          ></v-progress-circular>
        </v-row>
        <v-divider class="mt-1"></v-divider>
        <v-row
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
        </v-row>
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
      </v-container> -->
    </v-container>

    <!--提交按钮-->
    <div>
      <v-hover
          v-slot="{ hover }"
          open-delay="10">
        <v-btn
          v-if="degree !== 100"
          disabled
          x-large
        >Please complete the Questionnaire!
        </v-btn>
        <v-btn
          v-else
          :elevation="hover ? 10 : 2"
          :class="{ 'on-hover': hover }"
          color= #82A5D2
          x-large
          v-on:click="submit">Click to See the Output
        </v-btn>
      </v-hover>
    </div>
    <h1><br><br></h1>
    <h4>Copyright ©️ 2023 Lucky7</h4>

    <!--回到顶部-->
    <transition name="fade">
      <v-btn
        v-show="backTopShow"
        class="goTop"
        color=#5f7f9f
        fab
        mid
        dark
        @click="$vuetify.goTo(0, 'duration')">
        <v-icon large>mdi-chevron-up</v-icon>
      </v-btn>
    </transition>
  </v-app>
</template>
<script>

export default {
  name: 'QuesAsk',
  data() {
    return {
      nameID: '',
      question1: '',
      question2: '',
      question3: '',
      question4: '',
      question5: '',
      question6: '',
      question7: '',
      question8: '',
      question9: '',
      question10: '',
      question11: '',
      age: ['1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969',
        '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979',
        '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989',
        '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999',
        '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009',
        '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019',
        '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029',
        '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039'],
      tasks: [
        {done: false, text: 'Question1'},
        {done: false, text: 'Question2'},
        {done: false, text: 'Question3'},
        {done: false, text: 'Question4'},
        {done: false, text: 'Question5'},
        {done: false, text: 'Question6'},
        {done: false, text: 'Question7'},
        {done: false, text: 'Question8'},
        {done: false, text: 'Question9'},
        {done: false, text: 'Question10'},
        {done: false, text: 'Question11'}
      ],
      backTopShow: false,
      newTask: null,
      active_question: 0, // 激活题目的索引，从0开始
      degree: '', // 控制进度条
      num_question: 11 // 总问题数
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
          path: '/to-output',
          name: 'Output',
          params: {
            nameID: this.nameID,
            question1: this.question1,
            question2: this.question2,
            question3: this.question3,
            question4: this.question4,
            question5: this.question5,
            question6: this.question6,
            question7: this.question7,
            question8: this.question8,
            question9: this.question9,
            question10: this.question10,
            question11: this.question11,
            active_question: this.active_question
          }
        })
    },
    jump() {
      // 计算完成情况
      let count_ans = 0
      let flag = {
        question1: this.question1,
        question2: this.question2,
        question3: this.question3,
        question4: this.question4,
        question5: this.question5,
        question6: this.question6,
        question7: this.question7,
        question8: this.question8,
        question9: this.question9,
        question10: this.question10,
        question11: this.question11
      }
      for (let i = 0; i < 11; i++) {
        if (Object.values(flag)[i] !== '') {
          count_ans += 1
        }
      }
      // 跳转到下一个问题
      this.active_question = this.active_question + 1
      // 控制进度条
      this.degree = count_ans / this.num_question * 100
      // console.log(Object.values(flag)[6])
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
  top: 3.4%;
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
.v-radio__label {
  /* text-overflow: ellipsis; */
  white-space: pre-line;
}
</style>
