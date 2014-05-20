module.exports = function(grunt) {
  grunt.initConfig({
      less: {
          development: {
              options: {
                  paths: ["./gdlk/static/bower_components"],
                  yuicompress: true
              },
              files: {
                  "./gdlk/static/css/gdlk.css": "./less/base.less"
              }
          }
      },
      watch: {
          files: "./less/*",
          tasks: ["less"]
      }
  });
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-watch');
};
