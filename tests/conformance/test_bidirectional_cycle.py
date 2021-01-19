import pytest
from toggle.core.ModelLoader import bidirectional_cycle, ModelFile


def get_model_file(name, config):
  return ModelFile({"name": name, 'origin': 'local', 'type': 'machinecode'}, config)


def test_bidirectional_cycle(default_config):
  models = bidirectional_cycle()
  models.add(get_model_file("dolf", default_config))
  models.add(get_model_file("arnhold", default_config))
  assert (models.next().get_name() == "arnhold")
  assert (models.next().get_name() == "dolf")
  assert (models.next().get_name() == "arnhold")
  assert (models.prev().get_name() == "dolf")
  assert (models.count() == 2)
  assert ([model.get_name() for model in models] == ["dolf", "arnhold"])


def test_select_by_name(default_config):
  models = bidirectional_cycle()
  dolf = get_model_file("dolf", default_config)
  models.add(get_model_file("arnhold", default_config))
  models.add(get_model_file("sylvester", default_config))
  models.add(dolf)
  models.add(get_model_file("mr.t", default_config))
  assert (models.select_by_name("dolf") == dolf)
