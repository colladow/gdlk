(function(window, angular) {
  'use strict';

  var gdlk = angular.module('gdlk', ['ui.router', 'gdlk.combos']);

  gdlk.config(function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/');

    $stateProvider.state('index', {
      url: '/',
      templateUrl: '/static/js/home/index.html',
      controller: 'HomeController'
    });
  });

})(window, window.angular);
