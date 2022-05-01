module.exports = {
  content: [
      './app/templates/*.html',
      './app/templates/main/*.html',
      './app/templates/auth/*.html',
      './app/templates/dash/*.html',
      './app/templates/components/*.html'
  ],
  theme: {
    extend: {
      colors: {
        matrix_blue: {
          100: '#357DE9',
          200: '#104593'
        },
        matrix_gray: {
          100: '#7A7A7A',
          200: '#4F4F4F'
        }
      },
      fontFamily: {
        matrix_body: ['Nunito']
      }
    },
  },
  plugins: [],
}
