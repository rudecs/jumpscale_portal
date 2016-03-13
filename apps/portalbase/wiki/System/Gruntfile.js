module.exports = function(grunt) {

  grunt.initConfig({
    less: {
        development: {
          files: {
            ".files/css/flatTheme.css": ".files/less/flatTheme.less"
          }
        }
    },
    watch: {
        tasks: ["less"],
        options: {
          livereload: true,
        },
        files: ".files/less/*"
    },
  });

  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-less');

  grunt.registerTask('default', ['watch']);

};
