<template>
  <v-app>
    <!-- <v-parallax
      height="650"
      src="https://photo69.mac89.com/2020/10/29/02/29023015_d84ed4abc2_small.jpg"
    > -->
      <h1><br></h1>
      <v-row
        align="center"
        justify="center"
      >
        <v-img
          contain
          max-height="300"
          max-width="420"
          class="pa-0 secondary text-no-wrap rounded-pill"
          :src="DefaultImg"
        ></v-img>
      </v-row>
      <h2><br></h2>
      <v-row>
        <v-col class="text-center" cols="12">
          <v-divider></v-divider>
        </v-col>
      </v-row>
      <v-row
        align="center"
        justify="center"
      >
        <v-col class="text-center" cols="7">
        <v-form>
          <v-container>
              <v-text-field
                v-model="form.first"
                :rules="rules"
                counter
                required
                maxlength="50"
                hint="Please use only Chinese and punctuation"
                label="Please input the poem that you want to translate"
              ></v-text-field>
          </v-container>
        </v-form>
        </v-col>
      </v-row>
      <v-row
        align="center"
        justify="center"
      >
        <v-expansion-panels
          style="max-width: 700px"
          focusable
          hover
          accordion
        >
          <v-expansion-panel>
            <v-expansion-panel-header
              color=#e4ebec
            >
            <strong>
              {{"\xa0\xa0\xa0\xa0"}}System Function
            </strong>
            </v-expansion-panel-header>
            <v-expansion-panel-content
              color=#ebf5f0
              class="text-left"
            ><br>
              {{"\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0"}}· Jobviser is a career guidance and analysis website.<br>
              {{"\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0"}}· Jobviser recommends IDEAL JOBs according to the user's personal ability<br>
              {{"\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0"}}and requirements. <br>
              {{"\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0"}}· Meanwhile, Jobviser considers users' personalities to recommend SUITABLE JOBs<br>
              {{"\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0"}} that matchs users' characteristics. This will give the user new ideas for job hunting<br>
              {{"\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0"}}and provide analysis to help the user understand himself better.
            </v-expansion-panel-content>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-header
              color=#e4ebec
            >
            <strong>
              {{"\xa0\xa0\xa0\xa0"}}User Guide
            </strong>
            </v-expansion-panel-header>
            <v-expansion-panel-content
              color=#ebf5f0
              class="text-left"
            ><br>
              {{"\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0"}}1. Enter the user name;<br>
              {{"\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0"}}2. Agree to the term;<br>
              {{"\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0"}}3. Complete all 11 questions of the questionnaire;<br>
              {{"\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0"}}4. Click the submit button to view the results.
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-row>
      <h1><br></h1>
      <v-row
        align="center"
        justify="center"
      >
        <v-checkbox
          v-model="checkbox"
          :label="`This project may not always give exactly the right result, please be informed.`"
          color= #7aafa1
        ></v-checkbox>
      </v-row>
      <h1><br></h1>
      <v-row
        align="center"
        justify="center"
      >
        <v-hover
          v-slot="{ hover }"
          open-delay="10">
          <v-btn
            v-if="form.first === '' || checkbox === false"
            disabled
            x-large
          >Please input the poem
          </v-btn>
          <v-btn
            v-else
            :elevation="hover ? 10 : 2"
            :class="{ 'on-hover': hover }"
            color= #82A5D2
            x-large
            v-on:click="submit">See the Output{{ "\xa0\xa0" }}
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
        </v-hover>
      </v-row>
      <h1><br></h1>
      <h4>Copyright ©️ 2023 Lucky7</h4>
    <!-- </v-parallax> -->
  </v-app>
</template>

<script>
export default {
  name: 'Home',
  components: {},
  data () {
    const defaultForm = Object.freeze({
      first: ''
    })
    return {
      DefaultImg: require('../../static/logo3.png'),
      checkbox: false,
      form: Object.assign({}, defaultForm),
      rules: [val => (val || '').length > 0 || 'This field is required'],
      wordsRules: [v => v.trim().split(' ').length <= 5 || 'Max 5 words']
    }
  },
  computed: {
    formIsValid () {
      return (
        this.form.first
      )
    }
  },
  methods: {
    resetForm () {
      this.form = Object.assign({}, this.defaultForm)
      this.$refs.form.reset()
    },
    submit () {
      this.$router.push(
        {
          path: '/to-output',
          name: 'Output',
          params: {
            nameID: this.form.first
          }
        })
      this.snackbar = true
      this.resetForm()
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  color: #404863;
}
h2 {
  font-weight: normal;
}
h4 {
  font-weight: normal;
  color: #818181;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #306385;
}
</style>
