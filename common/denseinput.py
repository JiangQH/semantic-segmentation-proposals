import tensorflow as tf
from util import preprocess
class DenseInput(object):
    """
    a dense data layer. input is image, and pixel map
    """
    def __init__(self, config):
        self.batch_size = config.batch_size
        self.config = config

    def densedata_pipelines(self):
        # the name queue
        filename_queues = tf.train.string_input_producer([self.config.source], shuffle=True)
        # read the data in
        image, label, invalid_mask = self._file_reader(filename_queues)
        # return batch
        images, labels, invalid_masks = tf.train.batch([image, label, invalid_mask],
                                                       batch_size=self.config.batch_size,
                                                       num_threads=4,
                                                       capacity=50 + 3 * self.batch_size)
        return images, labels, invalid_masks

    def _file_reader(self, filename_queues):
        reader = tf.TextLineReader()
        _, serialized = reader.read(filename_queues)
        rgb_name, label_name = tf.decode_csv(serialized, [["path"], ["annotation"]])
        # read the image in
        img_file = tf.read_file(rgb_name)
        image = tf.image.decode_png(img_file, channels=3)
        # read the label in
        label_file = tf.read_file(label_name)
        label = tf.image.decode_png(label_file, channels=self.config.label_channel)
        # preprocess
        image, label, mask = preprocess(image, label, self.config)
        # get the invalid_mask
        # invalid_mask = tf.equal(label, [0, 0, 0])
        return image, label, mask


