(function(window, angular) {
  'use strict';

  var combos = angular.module('gdlk.combos', ['ui.router', 'gdlk.utils']);

  combos.config(function($stateProvider) {
    $stateProvider.state('combos', {
      abstract: true,
      url: '/combos',
      templateUrl: '/static/js/combos/base.html'
    })
      .state('combos.list', {
        url: '/list',
        templateUrl: '/static/js/combos/list.html',
        controller: 'ListController'
      })
      .state('combos.details', {
        url: '/{id:[0-9]+}',
        templateUrl: '/static/js/combos/details.html',
        controller: 'DetailsController'
      });
  });

})(window, window.angular);
