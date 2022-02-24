const pkg = require("./package");
import i18n from './config/i18n'

module.exports = {
  target: "static",

  router: {
    base: "/shop/"
  },

  /*
   ** Headers of the page
   */
  head: {
    title: pkg.description,
    meta: [
      { charset: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { hid: "description", name: "description", content: pkg.description },
      { "http-equiv": "x-ua-compatible", content: "ie=edge" },
      { name: "msapplication-TileColor", content: "#ffffff" },
      { name: "msapplication-TileImage", content: "/ms-icon-144x144.png" },
      { name: "theme-color", content: "#ffffff" },

      // Facebook open graph
      { property: "og:type", content: "website" },
      { property: "og:url", content: "https://example.com/page.html" },
      { property: "og:title", content: "Content Title" },
      { property: "og:image", content: "https://example.com/image.jpg" },
      { property: "og:description", content: "Description Here" },
      { property: "og:site_name", content: "Site Name" },
      { property: "og:locale", content: "en_US" },

      // Twitter card
      { property: "twitter:card", content: "summary" },
      { property: "twitter:site", content: "@site_account" },
      { property: "twitter:creator", content: "@individual_account" },
      { property: "twitter:url", content: "https://example.com/page.html" },
      { property: "twitter:title", content: "Content Title" },
      {
        property: "twitter:description",
        content: "Content description less than 200 characters"
      },
      { property: "twitter:image", content: "https://example.com/image.jpg" }
    ],
    link: [
      { rel: "icon", type: "image/x-icon", href: "/favicon.ico" },
      {
        rel: "stylesheet",
        href:
          "https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Material+Icons"
      },
      {
        rel: "stylesheet",
        integrity:
          "sha384-AYmEC3Yw5cVb3ZcuHtOA93w35dYTsvhLPVnYs9eStHfGJvOvKxVfELGroGkvsg+p",
        crossorigin: "anonymous",
        href: "https://pro.fontawesome.com/releases/v5.10.0/css/all.css"
      }
    ]
  },

  /*
   ** Customize the progress-bar color
   */
  loading: { color: "#fff" },

  /*
   ** Global CSS
   */
  css: ["bulma"],

  /*
   ** Plugins to load before mounting the App
   */
  plugins: [],

  /*
   ** Nuxt.js modules
   */
  modules: [
    '@nuxtjs/axios'
    // Doc: https://axios.nuxtjs.org/usage
  ],
    
  buildModules: [
  /* other modules */
  [
    'nuxt-i18n',
    {
      vueI18nLoader: true,
      defaultLocale: 'en',
      locales: [
        {
          code: 'en',
          name: 'English'
        },
        {
          code: 'de',
          name: 'Deutsch'
        }
      ],
      vueI18n: i18n
    }
  ]
  ],
  /*
   ** Axios module configuration
   */
  axios: {
    // See https://github.com/nuxt-community/axios-module#options
  },

  generate: {
    dir: "docs"
  }
};
