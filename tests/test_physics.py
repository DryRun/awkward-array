#!/usr/bin/env python

# Copyright (c) 2018, DIANA-HEP
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import unittest

import pytest
import numpy

import awkward

uproot_methods = pytest.importorskip("uproot_methods")

class Test(unittest.TestCase):
    def runTest(self):
        pass

    def test_physics_matching(self):
        gen_pt   = awkward.fromiter([[10.0, 20.0, 30.0],       [],     [40.0, 50.0]])
        reco_pt  = awkward.fromiter([[20.2, 10.1, 30.3, 50.5], [50.5], [50.5]])

        gen_eta  = awkward.fromiter([[-3.0, -2.0, 2.0],        [],     [-1.0, 1.0]])
        reco_eta = awkward.fromiter([[-2.2, -3.3, 2.2, 0.0],   [0.0],  [1.1]])

        gen_phi  = awkward.fromiter([[-1.5,  0.0, 1.5],        [],     [0.78, -0.78]])
        reco_phi = awkward.fromiter([[ 0.1, -1.4, 1.4, 0.78],  [0.78], [-0.77]])

        gen  = uproot_methods.TLorentzVectorArray.from_ptetaphim(gen_pt, gen_eta, gen_phi, 0.2)
        reco = uproot_methods.TLorentzVectorArray.from_ptetaphim(reco_pt, reco_eta, reco_phi, 0.2)

        print("gen", gen)
        print("reco", reco)

        print("gen.cross(reco)", gen.cross(reco))

        pairing = gen.cross(reco, nested=True)
        print("pairing = gen.cross(reco, nested=True)", gen.cross(reco))

        metric = pairing.i0.delta_r(pairing.i1)
        print("metric = pairing.i0.delta_r(pairing.i1", metric)

        index_of_minimized = metric.argmin()
        print("index_of_minimized = metric.argmin()", index_of_minimized)

        print("metric[index_of_minimized]", metric[index_of_minimized])

        passes_cut = (metric[index_of_minimized] < 0.5)
        print("passes_cut = (metric[index_of_minimized] < 0.5)", passes_cut)

        best_pairings_that_pass_cut = pairing[index_of_minimized][passes_cut]
        print("best_pairings_that_pass_cut = pairing[index_of_minimized][passes_cut]", best_pairings_that_pass_cut)

        genrecos = best_pairings_that_pass_cut.flatten(axis=1)
        print("genrecos = best_pairings_that_pass_cut.flatten(axis=1)", genrecos)

        print("genrecos.counts", genrecos.counts)
        print("gen.counts", gen.counts)

        print("genrecos.i0.pt", genrecos.i0.pt)
        print("genrecos.i1.pt", genrecos.i1.pt)


