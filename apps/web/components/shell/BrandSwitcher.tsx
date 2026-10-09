import type { BrandContext, BrandId, CommerceId } from "../../domain/types.ts";
import styles from "./shell.module.css";

export function BrandSwitcher({
  brands,
  brand,
  commerceId,
  onSelectBrand,
  onSelectCommerce,
}: {
  brands: BrandContext[];
  brand: BrandContext;
  commerceId: CommerceId | null;
  onSelectBrand: (id: BrandId) => void;
  onSelectCommerce: (id: CommerceId) => void;
}) {
  return (
    <section className={styles.switcher} aria-label="Espacio de trabajo">
      <div className={styles.identity}>
        <span className={styles.monogram} aria-hidden="true">{brand.name.charAt(0)}</span>
        <div>
          <p className={styles.identityName}>{brand.name}</p>
          <p className={styles.identityKind}>{brand.kind}</p>
        </div>
      </div>

      <div className={styles.field}>
        <label className={styles.fieldLabel} htmlFor="brand-select">Marca</label>
        <select
          id="brand-select"
          className={styles.select}
          value={brand.id}
          onChange={(event) => onSelectBrand(event.target.value as BrandId)}
        >
          {brands.map((option) => (
            <option key={option.id} value={option.id}>{option.name}</option>
          ))}
        </select>
      </div>

      {brand.commerceOptions ? (
        <div className={styles.field}>
          <label className={styles.fieldLabel} htmlFor="commerce-select">Comercio asociado</label>
          <select
            id="commerce-select"
            className={styles.select}
            value={commerceId ?? ""}
            onChange={(event) => onSelectCommerce(event.target.value as CommerceId)}
          >
            {brand.commerceOptions.map((option) => (
              <option key={option.id} value={option.id}>{option.name}</option>
            ))}
          </select>
        </div>
      ) : (
        <p className={styles.switcherNote}>Marca independiente · sin comercio asociado</p>
      )}
    </section>
  );
}
