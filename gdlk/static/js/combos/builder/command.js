(function(window, angular) {
  'use strict';

  var builder = angular.module('gdlk.combos.builder');

  builder.directive('command', function() {
    return {
      restrict: 'E',
      scope: {
        type: '@type',
        move: '@move'
      },
      transclude: true,
      template: '<span class="command" ng-class="[type, move]"></span>'
    };
  });

  builder.factory('Commands', function($http, httpUtils) {
    return httpUtils.checkStatusCode($http.get('/combos/commands'));
  });

})(window, window.angular);
