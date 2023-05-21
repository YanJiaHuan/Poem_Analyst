import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import QuesAsk from '@/components/QuesAsk'
import Output from '@/components/Output'
import Feedback from '@/components/Feedback'

Vue.use(Router)

const routes = [
  {
    path: '/',
    name: 'HelloWorld',
    component: HelloWorld,
    meta: {
      title: 'Main'
    }
  },
  {
    path: '/to-question',
    name: 'QuesAsk',
    component: QuesAsk,
    meta: {
      title: 'Question',
      keepAlive: true
    }
  },
  {
    path: '/to-output',
    name: 'Output',
    component: Output,
    meta: {
      title: 'Output'
    }
  },
  {
    path: '/to-feedback',
    name: 'Feedback',
    component: Feedback,
    meta: {
      title: 'Feedback'
    }
  }
]

const router = new Router({
  routes
})

router.beforeEach((to, from, next) => {
  /* 路由发生变化修改页面title */
  if (to.meta.title) {
    document.title = to.meta.title
  }
  next()
})

export default router

// export default new Router({
//   routes: [
//     {
//       path: '/',
//       name: 'HelloWorld',
//       component: HelloWorld
//     }
//   ]
// })
