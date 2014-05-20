(function(window, angular) {
  'use strict';

  var gdlk = angular.module('gdlk', ['ui.router', 'gdlk.combos']);

  gdlk.config(function($stateProvider) {
    $stateProvider.state('index', {
      url: '/',
      templateUrl: '/static/js/home/index.html',
      controller: 'HomeController'
    });
  });

})(window, window.angular);
