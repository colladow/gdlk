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
      template: '<div class="command" ng-class="[type, move]"></div>'
    };
  });

})(window, window.angular);
