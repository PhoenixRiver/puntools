#!/usr/bin/env python3

'''Data range checker for Naev.

Run this script from the root directory of your Naev source tree. It
reads the XML files in dat/ssys/ and dat/assets/ and gives details of
the ranges of values for certain statistics. Example usage:
user@home:~/naev/$ dataranges

'''

# Copyright © 2012 Tim Pederick, 2013 Johann Bryant.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# Standard library imports.
import math

# Local imports.
from dataloader import datafiles
from naevdata import SSystem, Asset

def stats(iterable):
    '''Find the mean and standard deviation of a data set.'''
    mean = sum(iterable) / len(iterable)
    sq_dists = list((i - mean) ** 2 for i in iterable)
    variance = sum(sq_dists) / len(sq_dists)
    std_dev = math.sqrt(variance)

    return mean, std_dev

def liststr(items):
    '''Format a list with commas and 'and'.'''
    if len(items) == 1:
        return str(items[0])
    else:
        return (', '.join(str(item) for item in items[:-1]) +
                ' and ' + str(items[-1]))

def hypot(x, y):
    '''Find the straightline distance of an asset in space.'''
    length = math.sqrt((x*x)+(y*y))

    return length

def main():
    ssystems = []
    for ssysfile in datafiles('SSystems'):
        # Parse each XML file into a SSystem object.
        ssystems.append(SSystem(ssysfile))

    neb_densest_at, neb_density, neb_densities = [], 0.0, []
    neb_worst_at, neb_volatility, neb_volatilities = [], 0.0, []
    int_worst_at, interference, interferences = [], 0.0, []

    largest_system, hi_radius, radii = [], 0.0, []
    smallest_system, lo_radius = [], float('Inf')

    most_stars_at, most_stars, stars = [], 0, []
    least_stars_at, least_stars = [], float('Inf')

    for ssys in ssystems:
        neb_densities.append(ssys.nebula.density)
        if ssys.nebula.density > neb_density:
            neb_densest_at, neb_density = [ssys.name], ssys.nebula.density
        elif ssys.nebula.density == neb_density:
            neb_densest_at.append(ssys.name)
        # ...else this isn't a candidate for the densest nebula.

        neb_volatilities.append(ssys.nebula.volatility)
        if ssys.nebula.volatility > neb_volatility:
            neb_worst_at, neb_volatility = [ssys.name], ssys.nebula.volatility
        elif ssys.nebula.volatility == neb_volatility:
            neb_worst_at.append(ssys.name)
        # ...else this isn't a candidate for the most dangerous nebula.

        interferences.append(ssys.interference)
        if ssys.interference > interference:
            int_worst_at, interference = [ssys.name], ssys.interference
        elif ssys.interference == interference:
            int_worst_at.append(ssys.name)
        # ...else this isn't a candidate for the highest interference.

        radii.append(ssys.radius)
        if ssys.radius > hi_radius:
            largest_system, hi_radius = [ssys.name], ssys.radius
        elif ssys.radius == hi_radius:
            largest_system.append(ssys.name)
        # ...else this isn't a candidate for the largest system.
        if ssys.radius < lo_radius:
            smallest_system, lo_radius = [ssys.name], ssys.radius
        elif ssys.radius == lo_radius:
            smallest_system.append(ssys.name)
        # ...else this isn't a candidate for the smallest system.

        stars.append(ssys.stars)
        if ssys.stars > most_stars:
            most_stars_at, most_stars = [ssys.name], ssys.stars
        elif ssys.stars == most_stars:
            most_stars_at.append(ssys.name)
        # ...else this isn't a candidate for the starriest system.
        if ssys.stars < least_stars:
            least_stars_at, least_stars = [ssys.name], ssys.stars
        elif ssys.stars == least_stars:
            least_stars_at.append(ssys.name)
        # ...else this isn't a candidate for the least starry system.

    print('Radius: μ={}, σ={}'.format(*stats(radii)))
    print('The largest system radius',
          '({}) is found in {}.'.format(hi_radius, liststr(largest_system)))
    print('The smallest system radius',
          '({}) is found in {}.'.format(lo_radius, liststr(smallest_system)))
    print()
    print('Nebula density: μ={}, σ={}'.format(*stats(neb_densities)))
    print('The densest nebula ({}) is in {}.'.format(neb_density,
                                                     liststr(neb_densest_at)))
    print()
    print('Nebula volatility: μ={}, σ={}'.format(*stats(neb_volatilities)))
    print('The nebula is at its most volatile',
          '({}) in {}.'.format(neb_volatility, liststr(neb_worst_at)))
    print()
    print('Interference: μ={}, σ={}'.format(*stats(interferences)))
    print('Interference is at its peak',
          '({}) in {}.'.format(interference, liststr(int_worst_at)))
    print()
    print('Stars: μ={}, σ={}'.format(*stats(stars)))
    print('The most starry skies',
          '({}) are found in {}.'.format(most_stars, liststr(most_stars_at)))
    print('The least starry skies',
          '({}) are found in {}.'.format(least_stars, liststr(least_stars_at)))
    print()

    assets = []
    for assetsfile in datafiles('Assets'):
        # Parse each XML file into a Asset object.
        assets.append(Asset(assetsfile))

    furthest, hi_orbit, orbits = [], 0.0, []
    nearest, lo_orbit = [], float('Inf')

    best_hidden, hi_hide, hides = [], 0.0, []
    worst_hidden, lo_hide = [], float('Inf')
    
    most_pop, hi_pop, pops = [], 0.0, []
    least_pop, lo_pop, total_pops = [], float('Inf'), []
    
    for asset in assets:
        if not asset.virtual:
            orbit = hypot(asset.pos.x, asset.pos.y)
            orbits.append(orbit)
            if orbit > hi_orbit:
                furthest, hi_orbit = [asset.name], orbit
            elif orbit == hi_orbit:
                furthest.append(asset.name)
            # ...else this isn't a candidate for the biggest orbit.
            if orbit < lo_orbit:
                nearest, lo_orbit = [asset.name], orbit
            elif orbit == lo_orbit:
                nearest.append(asset.name)
            # ...else this isn't a candidate for the smallest orbit.

            hides.append(asset.hide)
            if asset.hide > hi_hide:
                best_hidden, hi_hide = [asset.name], asset.hide
            elif asset.hide == hi_hide:
                best_hidden.append(asset.name)
            # ...else this isn't a candidate for the biggest population.
            if asset.hide < lo_hide:
                worst_hidden, lo_hide = [asset.name], asset.hide
            elif asset.hide == lo_hide:
                worst_hidden.append(asset.name)
            # ...else this isn't a candidate for the smallest population.

            total_pops.append(asset.population)
            if asset.population > 0:
                pops.append(asset.population)
                if asset.population > hi_pop:
                    most_pop, hi_pop = [asset.name], asset.population
                elif asset.population == hi_pop:
                    most_pop.append(asset.name)
                # ...else this isn't a candidate for the biggest population.
                if asset.population < lo_pop:
                    least_pop, lo_pop = [asset.name], asset.population
                elif asset.population == lo_pop:
                    least_pop.append(asset.name)
                # ...else this isn't a candidate for the smallest population.

    print('Orbit: μ={}, σ={}'.format(*stats(orbits)))
    print('The biggest orbit',
          '({}) is {}.'.format(hi_orbit, liststr(furthest)))
    print('The smallest orbit',
          '({}) is {}.'.format(lo_orbit, liststr(nearest)))
    print()
    print('Difficulty in sensing: μ={}, σ={}'.format(*stats(hides)))
    print('The best hidden',
          '({}) is {}.'.format(hi_hide, liststr(best_hidden)))
    print('The worst hidden',
          '({}) is {}.'.format(lo_hide, liststr(worst_hidden)))
    print()
    print('Population (everywhere): μ={}, σ={}'.format(*stats(total_pops)))
    print('Population (inhabitted only): μ={}, σ={}'.format(*stats(pops)))
    print('The biggest population',
          '({}) is in {}.'.format(hi_pop, liststr(most_pop)))
    print('The smallest population (greater than zero)',
          '({}) is in {}.'.format(lo_pop, liststr(least_pop)))
    print()

if __name__ == '__main__':
    main()