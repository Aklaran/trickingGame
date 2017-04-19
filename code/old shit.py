# define actor intervals

class OldShit(Object):
    def __init__(self):
        self.tricker.gainer = Sequence(
            self.tricker.actorInterval('gainer', startFrame=1, endFrame=10),
            Parallel(self.tricker.posInterval(0.6,
                                              Point3(0, .1, 0),
                                              other=self.tricker),
                     self.tricker.actorInterval('gainer', startFrame=10, endFrame=34)
                     )
        )

        self.tricker.gswitch = Sequence(
            self.tricker.actorInterval('gswitch', startFrame=1, endFrame=7),
            Parallel(self.tricker.posInterval(0.46,
                                              Point3(0, .1, 0),
                                              other=self.tricker),
                     self.tricker.actorInterval('gswitch', startFrame=7, endFrame=21)
                     )
        )