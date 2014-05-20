(function(window, angular) {
  'use strict';

  var combos = angular.module('gdlk.combos', ['ui.router']);

  combos.config(function($stateProvider) {
    $stateProvider.state('combos', {
      url: '/combos',
      templateUrl: '/static/js/combos/list.html',
      controller: 'ListController'
    });
  });

})(window, window.angular);
