(function(window, angular) {
  'use strict';

  var combos = angular.module('gdlk.combos');

  combos.controller('ListController', function($scope, Combo) {
    Combo.query().then(function(combos) {
      $scope.combos = combos;
    });;
  });

})(window, window.angular);
