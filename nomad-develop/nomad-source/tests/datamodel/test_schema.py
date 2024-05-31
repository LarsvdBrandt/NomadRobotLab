#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os.path
import pytest

from nomad.metainfo import MetainfoError
from nomad.datamodel.context import ServerContext
from nomad.datamodel.datamodel import EntryArchive, EntryMetadata
from nomad.datamodel.data import UserReference, AuthorReference
from nomad.datamodel.metainfo.annotations import valid_eln_types, valid_eln_components
from nomad.parsing.parser import ArchiveParser
from nomad.processing.data import Upload
from nomad.utils import get_logger, strip

from tests.normalizing.conftest import run_normalize
from tests.test_files import create_test_upload_files
from tests.metainfo.test_yaml_schema import yaml_to_package


def test_schema_processing(raw_files_function, no_warn):
    directory = os.path.join(os.path.dirname(__file__), '../data/datamodel')
    mainfile = 'schema.archive.json'

    # create upload with example files
    upload_files = create_test_upload_files(
        'test_upload_id', published=False, raw_files=directory
    )
    upload = Upload(upload_id='test_upload_id')

    # parse
    parser = ArchiveParser()
    context = ServerContext(upload=upload)
    test_archive = EntryArchive(m_context=context, metadata=EntryMetadata())
    parser.parse(upload_files.raw_file_object(mainfile).os_path, test_archive)
    run_normalize(test_archive)

    # assert archive
    assert len(test_archive.definitions.section_definitions) == 1
    assert test_archive.metadata.entry_type == 'Schema'


def test_eln_annotation_validation_parsing(raw_files_function, caplog):
    mainfile = os.path.join(
        os.path.dirname(__file__), '../data/datamodel/eln.archive.yaml'
    )

    # parse
    parser = ArchiveParser()
    test_archive = EntryArchive(metadata=EntryMetadata())
    with pytest.raises(Exception):
        parser.parse(mainfile, test_archive, get_logger(__name__))

    has_error = False
    for record in caplog.get_records(when='call'):
        if record.levelname == 'ERROR':
            has_error = True

    assert has_error


@pytest.mark.parametrize('eln_type', valid_eln_types.keys())
@pytest.mark.parametrize('eln_component', sum(valid_eln_components.values(), []))
def test_eln_annotation_validation(eln_type, eln_component):
    base_schema = strip(
        """
        m_def: 'nomad.metainfo.metainfo.Package'
        sections:
            Sample:
                base_section: 'nomad.datamodel.data.EntryData'
                quantities:
                    sample_id:
                        type: str
                        m_annotations:
                            eln:
                                component: StringEditQuantity
            Process:
                base_section: 'nomad.datamodel.data.EntryData'
                quantities:
                    quantity_name:
                        type: quantity_type
                        m_annotations:
                            eln:
                                component: eln_component
    """
    )

    for quantity_type in valid_eln_types[eln_type]:
        if eln_type == 'reference':
            yaml_schema = base_schema.replace('quantity_type', "'#/Sample'").replace(
                'eln_component', eln_component
            )
        else:
            yaml_schema = base_schema.replace('quantity_type', quantity_type).replace(
                'eln_component', eln_component
            )

        if eln_component not in valid_eln_components[eln_type]:
            package = yaml_to_package(yaml_schema)
            type_name = quantity_type
            if eln_type in ['number', 'datetime', 'enum', 'reference']:
                quantity = package['section_definitions'][1]['quantities'][0]
                if type(quantity.type).__name__ != 'type':
                    type_name = type(quantity.type).__name__
            with pytest.raises(Exception) as exception:
                package.__init_metainfo__()

            assert isinstance(exception.value, MetainfoError)
            error_str = (
                f'The component {eln_component} '
                f'is not compatible with the quantity quantity_name of the type {type_name}. '
                f'Accepted components: {", ".join(valid_eln_components[eln_type])}'
            )
            assert error_str in exception.value.args[0]


def test_user_author_yaml_deserialization():
    des_m_package = yaml_to_package(
        strip(
            """
        m_def: 'nomad.metainfo.metainfo.Package'
        sections:
            Sample:
                base_section: 'nomad.datamodel.metainfo.measurements.Sample'
                quantities:
                    my_user:
                        type: User
                        m_annotations:
                            eln:
                                component: AuthorEditQuantity
                    my_author:
                        type: Author
                        m_annotations:
                            eln:
                                component: AuthorEditQuantity
    """
        )
    )
    des_sample = des_m_package['section_definitions'][0]
    des_my_user = des_sample.quantities[0]
    des_my_author = des_sample.quantities[1]

    assert des_my_user.name == 'my_user'
    assert des_my_author.name == 'my_author'
    assert isinstance(des_my_user.type, UserReference)
    assert isinstance(des_my_author.type, AuthorReference)
