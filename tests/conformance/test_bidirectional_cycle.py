import pytest
from toggle.core.ModelLoader import bidirectional_cycle, ModelFile


def get_model_file(name):
  return ModelFile({"name": name, 'origin': 'local'}, "")


def test_bidirectional_cycle():
  models = bidirectional_cycle()
  models.add(get_model_file("dolf"))
  models.add(get_model_file("arnhold"))
  assert (models.next().get_name() == "arnhold")
  assert (models.next().get_name() == "dolf")
  assert (models.next().get_name() == "arnhold")
  assert (models.prev().get_name() == "dolf")
  assert (models.count() == 2)
  assert ([model.get_name() for model in models] == ["dolf", "arnhold"])


def test_select_by_name():
  models = bidirectional_cycle()
  dolf = get_model_file("dolf")
  models.add(get_model_file("arnhold"))
  models.add(get_model_file("sylvester"))
  models.add(dolf)
  models.add(get_model_file("mr.t"))
  assert (models.select_by_name("dolf") == dolf)
