<div style="width: 100%; height: 100%; display: flex; justify-content: center;">
  <div style="width: 75%; border: 2px solid #BB3333; background-color: #EE9999; padding: 8px 12px; color: black">
    <h1 style="border-bottom: 0; text-align: center;">Note</h1><p><a href="https://github.com/esi/esi-docs" style="color: #000000">ESI-Docs</a> has moved to <a href="https://developers.eveonline.com/docs/" style="font-weight: 700; color: #000000;">a new home</a>. This content will remain available for now, but will no longer be updated. Please update your bookmarks.
    </p>
  </div>
</div>

# Static Data Export

The [Static Data Export (SDE)](https://developers.eveonline.com/resource/resources) is a CCP provided snapshot of static data used in EVE Online. A new version is typically released after every patch which changes the static data, though this may be delayed for various reasons.

It is provided as a ZIP archive containing many YAML files describing different aspects of EVE's static data, with some information encoded in the folder structure.

As the exact format of the data in the SDE often changes, it isn't detailed in this documentation. If you are looking to use the SDE, consider using one of the available [SDE Conversions](sde_conversions.md). If the SDE doesn't contain the static data you require, read the documentation on [SDE Complements](sde_complements.md).
