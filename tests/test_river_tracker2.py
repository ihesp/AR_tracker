'''Test tracking in river_tracker2.
'''


#--------Import modules-------------------------
from __future__ import print_function
import os
import unittest
# try fixing the issue of
# _tkinter.TclError: no display name and no $DISPLAY environment variable
import matplotlib
matplotlib.use('Agg')
from ipart.AR_tracer import readCSVRecord, trackARs, filterTracks


class TestDetect(unittest.TestCase):
    """Test input netcdf data"""

    def setUp(self):

        thisdir=os.path.dirname(__file__)
        fixture_dir=os.path.join(thisdir, 'fixtures')
        abpath_in=os.path.join(fixture_dir,'sample_record.csv')
        self.ardf=readCSVRecord(abpath_in)

        self.time_gap_allow=6
        self.num_anchors=7
        self.track_scheme='simple'
        self.max_dist_allow=1200
        self.min_duration=24
        self.min_nonrelax=1

    def test_track(self):

        self.assertTupleEqual(self.ardf.shape, (99,22),
                "Input <ardf> shape wrong.")

        #-------------------Track ars-------------------
        track_list=trackARs(self.ardf, self.time_gap_allow,
                self.max_dist_allow, self.track_scheme,
                isplot=False, verbose=False)
        self.assertEqual(len(track_list), 19, "Number of tracks wrong.")

        #------------------Filter tracks------------------
        track_list=filterTracks(track_list, self.min_duration,
                self.min_nonrelax)
        self.assertEqual(len(track_list), 7, "Number of filtered tracks wrong.")

        nums=[len(track_list[ii].data) for ii in range(len(track_list))]
        ans=(5, 12, 11, 21, 11, 11, 5)
        self.assertTupleEqual(tuple(nums), ans, "Track lengths wrong.")


if __name__=='__main__':

    unittest.main()





